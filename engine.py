from collections import deque


def evaluate(data):
    quotas, window = data["quotas"], data["window"]
    if type(window) is not int or window < 1 or not quotas or any(type(v) is not int or v < 1 for v in quotas.values()):
        raise ValueError("window and quotas must be positive")
    tenants = deque(sorted(quotas))
    queues = {t: deque() for t in tenants}
    seen = set()
    for job in sorted(data["jobs"], key=lambda j: j["arrival"]):
        at, name, tenant = job["arrival"], job["id"], job["tenant"]
        if type(at) is not int or at < 0 or tenant not in queues or name in seen:
            raise ValueError("invalid or repeated job")
        seen.add(name)
        queues[tenant].append(job)
    clock = 0
    used = {}
    epoch = -1
    result = []
    while len(result) < len(seen):
        if clock // window != epoch:
            epoch, used = clock // window, {}
        next_times = []
        for _ in range(len(tenants)):
            tenant = tenants[0]
            tenants.rotate(-1)
            if not queues[tenant]:
                continue
            job = queues[tenant][0]
            available = job["arrival"]
            if used.get(tenant, 0) >= quotas[tenant]:
                available = max(available, (epoch + 1) * window)
            if available > clock:
                next_times.append(available)
                continue
            queues[tenant].popleft()
            used[tenant] = used.get(tenant, 0) + 1
            result.append({"id": job["id"], "tenant": tenant, "tick": clock, "wait": clock-job["arrival"]})
            clock += 1
            break
        else:
            clock = min(next_times)
    return result
