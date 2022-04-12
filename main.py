
with open('device_id.txt') as f:
    device_id = f.readline().rstrip()

v1 = ["01", "03", "04", "05", "06"]

if device_id in v1:
    from version import v1
    # v1()
else:
    from version import v2
    # v2()