from importlib import import_module

enabled_days = range(1, 9)

for day in enabled_days:
    import_module(f'Day{day}').run()
