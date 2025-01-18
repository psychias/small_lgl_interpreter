from datetime import datetime
import sys


def parse_data(lines):
    return [
        {
            'unique_id': int(id),
            'function_name': func,
            'event': start_stop,
            'timestamp': datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        }
        for line in lines[1:]
        for id, timestamp,func, start_stop in [line.rstrip().split(',')]
    ]


def call_stack(data):
    function_calls = {}
    for row in data:
        func_data = function_calls.setdefault(row['function_name'], {'start_time': None, 'total_time': 0, 'calls_counter': 0})

        if row['event'] == 'start':
            func_data['start_time'] = row['timestamp']
        elif row['event']  == 'stop' and func_data['start_time'] is not None:
            func_data['total_time'] += (row['timestamp'] - func_data['start_time']).total_seconds() * 1000
            func_data['calls_counter'] += 1
            func_data['start_time'] = None  

    return function_calls


def print_table(function_calls):
    header = "| Function Name     | Num. of calls  | Total Time (ms) | Average Time (ms)|"
    sep = "|-------------------------------------------------------------------------|"
    
    print(header)
    print(sep)

    row_template = "| {name:<17} | {calls:^14} | {total:.3f} ms       | {average:.3f} ms        |"

    for function_name, stats in function_calls.items():
        calls_counter = stats['calls_counter']
        total_time = stats['total_time']
        average_time = total_time / calls_counter if calls_counter > 0 else 0

        print(row_template.format(
            name=function_name,
            calls=str(calls_counter),
            total=total_time,
            average=average_time
        ))

    
def main():
    
    log_file = sys.argv[-1]

    with open(log_file, "r") as file:
        lines = file.readlines()
    print()
    data = parse_data(lines)
    calls = call_stack(data)
    table = print_table(calls)
    print()
    

if __name__ == "__main__":
    main()