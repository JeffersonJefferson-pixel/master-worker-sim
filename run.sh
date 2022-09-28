until [ "`docker inspect -f {{.State.Running}} simgrid`"=="true" ]; do
    sleep 0.1;
done;
# run simulation and generate visualization
docker exec --user 0:0 -it simgrid bash -c "cd /source/tutorial;python master-workers.py small_platform.xml master-workers_d.xml --cfg=tracing:yes --cfg=tracing/actor:yes;Rscript draw_gantt.R simgrid.trace;"