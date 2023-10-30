#!/bin/bash
mode=$1
dbt_target=$2
dbt_models=$3
dbt_vars=$4
full_refresh=$5

cd /dbt

if [ $mode = "run" ]; then
    echo "dbt Mode is run"
    if [ $full_refresh = "True" ]; then
        echo "Doing a full refresh"
        dbt run --target="$dbt_target" --select="$dbt_models" --vars="$dbt_vars"  --full-refresh
    else
        echo "Not doing a full refresh"
        dbt run --target="$dbt_target" --select="$dbt_models" --vars="$dbt_vars" 
    fi
elif [ $mode = "debug" ]; then
    echo "dbt Mode is debug"
    dbt debug  --target="$dbt_target"
elif [ $mode = "deps" ]; then
    echo "dbt Mode is dept"
    dbt deps
elif [ $mode = "test" ]; then
    echo "dbt Mode is test"
    dbt test    
elif [ $mode = "local" ]; then
    echo "dbt local run"
    dbt run --target="$dbt_target" --select="$dbt_models" --vars="$dbt_vars" --project-dir=/Users/lufengsh/Documents/GitHub/dbt-demo/demo
else      
    echo "Incorrect dbt Mode. Nothing to do"
fi

# this is a test
# so that the final exit code form removing virtualenv cmd doesn't get used by KubernetesPodOperator 
exit_code=$?

# rethrowing the exit code to KubernetesPodOperator
exit $exit_code 

