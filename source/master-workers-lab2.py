from simgrid import Actor, Engine, Host, Mailbox, this_actor
import sys

# global
e = Engine(sys.argv)

# master-begin
def master(*args):
    assert len(args) == 3, f"Actor master requires 3 parameters, but got {len(args)}"
    
    tasks_count = int(args[0])
    # each task has same compute cost
    compute_cost = int(args[1])
    communicate_cost = int(args[2])
    workers = []

    # get mailbox of workers
    # workerId: [0, worker_count-1]
    
    # get all hosts
    hosts = e.all_hosts
    # create worker actors with master
    for i, host in enumerate(hosts):
        # give name based on id
        # worker take id as args
        Actor.create(f"worker", host, worker, i)

    worker_count = len(hosts)
    for i, _ in enumerate(hosts):
        workers.append(Mailbox.by_name(str(i)))
    this_actor.info(f"Got {len(workers)} workers and {tasks_count} tasks to process")

    for i in range(tasks_count): # For each task to be executed: 
        # - Select a worker in a round-robin way
        mailbox = workers[i % worker_count]

        # - Send the computation amount to the worker
        # 1 task at a time
        if (tasks_count < 10000 or (tasks_count < 100000 and i % 10000 == 0) or i % 100000 == 0):
            this_actor.info(f"Sending task {i} of {tasks_count} to mailbox '{mailbox.name}'")
        # since allocate 1 task at a time and each task has same compute_cost
        # only care about compute cost
        mailbox.put(compute_cost, communicate_cost)

    this_actor.info("All tasks have been dispatched. Request all workers to stop.")
    for i in range(len(workers)):
        # The workers stop when receiving a negative compute_cost
        mailbox = workers[i]
        mailbox.put(-1, 0)
# master-end

# worker-begin
def worker(*args):
    # get name from args
    name = str(args[0])
    mailbox = Mailbox.by_name(name)
    done = False
    while not done:
        # only care about compute cost
        compute_cost = mailbox.get()
        if compute_cost > 0: # If compute_cost is valid, execute a computation of that cost 
            this_actor.execute(compute_cost)
        else: # Stop when receiving an invalid compute_cost
            done = True
    
    this_actor.info("Exiting now.")
# worker-end

# main-begin
if __name__ == '__main__':
    assert len(sys.argv) > 2, f"Usage: python app-masterworkers.py platform_file deployment_file"
    
    # Register the classes representing the actors
    e.register_actor("master", master)
    e.register_actor("worker", worker)

    # Load the platform description and then deploy the application
    e.load_platform(sys.argv[1]) 
    e.load_deployment(sys.argv[2])

    # Run the simulation
    e.run()

    this_actor.info("Simulation is over")
# main-end
