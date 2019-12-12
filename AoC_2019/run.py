import timeit
from importlib import import_module

days_times = {}
for day in range(1, 25):
    try:
        days_times[day] = timeit.timeit(lambda: import_module(f'Day{day}').run(False), number=1)
    except ModuleNotFoundError:
        break
    except Exception as e:
        print('Day {day} failed : {e} !')

total_time = 0
for day, day_time in days_times.items():
    total_time += day_time
    print(f'>> Day {day} took {day_time:0.3f}s')

print(f'>> Total took {total_time:0.3f}s')
