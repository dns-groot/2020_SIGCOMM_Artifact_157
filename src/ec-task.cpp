#include "ec-task.h"
#include "job.h"

string ECTask::PrintTaskType()
{
    return "EC Task";
}

void ECTask::Process(const Context &context, vector<boost::any> &variadic_arguments)
{
    Job *current_job = boost::any_cast<Job *>(variadic_arguments[0]);
    interpretation::Graph interpretation_graph_for_ec(ec_, context);
    interpretation_graph_for_ec.CheckForLoops(current_job->json_queue);
    // interpretation_graph_for_ec.GenerateDotFile("InterpretationGraph.dot");
    current_job->attributes_queue.enqueue(
        {static_cast<int>(num_vertices(interpretation_graph_for_ec)),
         static_cast<int>(num_edges(interpretation_graph_for_ec))});
    current_job->stats.ec_count++;
    interpretation_graph_for_ec.CheckPropertiesOnEC(
        current_job->path_functions, current_job->node_functions, current_job->json_queue);
}
