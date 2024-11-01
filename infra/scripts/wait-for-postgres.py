import subprocess


def check_postgres():
    result = subprocess.run(
        [
            'docker',
            'exec',
            'postgres-dev',
            'pg_isready',
            '--host',
            'localhost',
        ],
        capture_output=True,
        text=True,
        timeout=10000,
        check=False,
    )
    if result.returncode != 0 and 'accepting connections' not in result.stdout:
        check_postgres()
        return
    print('\n🟢 Postgres está pronto e aceitando conexões\n')


if __name__ == '__main__':
    print('\n🟡 Aguardando Postgres aceitar conexões')
    check_postgres()
