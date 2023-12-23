import subprocess
import shlex


def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    command: str = f'ps -u {shlex.quote(username)} | wc -l'
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as proc:
        proc.wait(timeout=1)
        if proc.returncode != 1:
            x = proc.communicate(timeout=1)[0].strip()
            if x.isdigit():
                return int(x) - 1


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    command: str = f'ps --ppid {root_pid} -o %mem'
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as proc:
        proc.wait(timeout=1)
        if proc.returncode == 0:
            pids = proc.communicate(timeout=1)[0].strip()[5:].split('\n')
            return sum(float(i) for i in pids)


if __name__ == '__main__':
    total_users_procs = process_count('root')
    total_memory = total_memory_usage(1)

    print(f'количество процессов, запущенных из-под текущего пользователя username {total_users_procs}',
          f'суммарное потребление памяти древа процессов  с корнем root_pid в процентах '
          f'{total_memory:.2f} % mem', sep='\n')
