lab_num=${1:-0}
# default is 0
echo "Lab: $lab_num";

deploy_file="master-workers_d.xml";
sim_file="master-workers.py";

if [ "$lab_num" == 1 ]; then
    deploy_file="master-workers-d-lab1.xml"
    sim_file="master-workers-lab1.py"
fi

until [ "`docker inspect -f {{.State.Running}} simgrid`"=="true" ]; do
    sleep 0.1;
done;
# run simulation and generate visualization
docker exec --user 0:0 -it simgrid bash -c "cd /source/tutorial;python $sim_file small_platform.xml $deploy_file --cfg=tracing:yes --cfg=tracing/actor:yes;Rscript draw_gantt.R simgrid.trace;"