def build_jobs(speed, degrees):
    seconds = degrees / speed

    jobs = []
    for i in range(seconds * 60):
        jobs.append(MoveJob())
