## volume mount
DIRECTORY="./source"

if [ ! -d "$DIRECTORY" ]; then
    echo "$DIRECTORY does not exist.";
    mkdir $DIRECTORY;
fi

if [ -z "$(ls -A $DIRECTORY)" ]; then
    echo "Empty";
    until [ "`docker inspect -f {{.State.Running}} simgrid`"=="true" ]; do
        sleep 0.1;
    done;
    docker exec --user 0:0 -it simgrid bash -c "cp -r /source/simgrid-template-s4u.git/* /source/tutorial;cd /source/tutorial;cmake .;make;";
fi