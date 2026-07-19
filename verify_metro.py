import json

with open(r'data/metro_status.json') as f:
    data = json.load(f)

print(f'Total entries: {len(data)}')
print()

lines = set(r['line'] for r in data)
print(f'Lines present: {sorted(lines)}')

statuses = {}
for r in data:
    s = r['status']
    statuses[s] = statuses.get(s, 0) + 1
print(f'Status counts: {statuses}')

delayed = [r for r in data if r['status'] == 'Delayed']
print(f'Delayed entries: {len(delayed)}')
for d in delayed:
    print(f'  line={d["line"]}, delay_minutes={d["delay_minutes"]} (should be 3-15)')

suspended = [r for r in data if r['status'] == 'Suspended']
print(f'Suspended entries: {len(suspended)}')
for s in suspended:
    print(f'  line={s["line"]}, delay_minutes={s["delay_minutes"]} (should be 0)')

on_time_wrong = [r for r in data if r['status'] == 'On Time' and r['delay_minutes'] != 0]
print(f'On Time with non-zero delay (should be empty): {on_time_wrong}')

timestamps = set(r['timestamp'] for r in data)
print(f'Timestamps: {sorted(timestamps)}')

entries = [(r['timestamp'], r['line']) for r in data]
print(f'Duplicate (timestamp, line) pairs: {len(entries) - len(set(entries))}')

fields_ok = all(
    'timestamp' in r and 'line' in r and 'delay_minutes' in r and 'status' in r and 'next_arrival' in r
    for r in data
)
print(f'All required fields present: {fields_ok}')

print()
checks = [
    len(data) >= 20,
    len(delayed) >= 3,
    len(suspended) >= 1,
    len(on_time_wrong) == 0,
    fields_ok,
    len(entries) - len(set(entries)) == 0,
]
if all(checks):
    print('All checks PASSED!')
else:
    print('SOME CHECKS FAILED!')
