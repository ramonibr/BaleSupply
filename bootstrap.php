<?php

declare(strict_types=1);

use App\Core\App;
use App\Core\Database;

if (!defined('BASE_PATH')) {
    define('BASE_PATH', __DIR__);
}

if (!function_exists('base_path')) {
    function base_path(string $path = ''): string
    {
        return BASE_PATH . ($path !== '' ? DIRECTORY_SEPARATOR . ltrim($path, DIRECTORY_SEPARATOR) : '');
    }
}

function load_env(string $envFile): void
{
    if (!is_file($envFile)) {
        return;
    }

    $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if ($lines === false) {
        return;
    }

    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#')) {
            continue;
        }

        [$key, $value] = array_pad(explode('=', $line, 2), 2, '');
        $key = trim($key);
        $value = trim($value);

        if ($key === '') {
            continue;
        }

        if ($value !== '' && (
            (str_starts_with($value, '"') && str_ends_with($value, '"')) ||
            (str_starts_with($value, "'") && str_ends_with($value, "'"))
        )) {
            $value = substr($value, 1, -1);
        }

        $_ENV[$key] = $value;
        $_SERVER[$key] = $value;
        putenv($key . '=' . $value);
    }
}

load_env(base_path('.env'));

spl_autoload_register(static function (string $class): void {
    $prefix = 'App\\';
    if (!str_starts_with($class, $prefix)) {
        return;
    }

    $relative = substr($class, strlen($prefix));
    $file = base_path('app/' . str_replace('\\', '/', $relative) . '.php');

    if (is_file($file)) {
        require $file;
    }
});

require base_path('app/Core/helpers.php');

$config = [
    'app' => require base_path('config/app.php'),
    'database' => require base_path('config/database.php'),
];

App::set('config', $config);

date_default_timezone_set((string) config('app.timezone', 'UTC'));

if (is_dir(base_path('storage/sessions'))) {
    session_save_path(base_path('storage/sessions'));
}

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_start();
}

App::set('db', new Database($config['database']));

set_exception_handler(static function (Throwable $exception): void {
    $message = sprintf(
        '[%s] %s in %s:%d%s',
        date('Y-m-d H:i:s'),
        $exception->getMessage(),
        $exception->getFile(),
        $exception->getLine(),
        PHP_EOL
    );

    @file_put_contents(base_path('storage/logs/app.log'), $message, FILE_APPEND);

    http_response_code(500);

    if (config('app.debug', false)) {
        echo '<h1>500 Internal Server Error</h1>';
        echo '<pre>' . e((string) $exception) . '</pre>';
        return;
    }

    echo '<h1>500 Internal Server Error</h1>';
});
