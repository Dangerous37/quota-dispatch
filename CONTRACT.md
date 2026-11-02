# Scheduler contract
quotas maps tenant to a positive integer count per fixed window; window is its length in integer ticks. jobs are unique IDs with tenant and nonnegative arrival tick. Each tick has one global dispatch slot. Among eligible tenants use round robin, preserving FIFO per tenant. Windows start at tick zero. Output includes dispatch tick and queue delay.
