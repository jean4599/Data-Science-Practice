#include <set>
#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <cstring>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <csignal>

using namespace std;
using Node = int;
using NodeSet = set<Node>;
using Graph = map<Node, NodeSet>;

NodeSet maximum_clique;
string input_file;
string output_file;
// class BronKerbosch{
// 	public:
// 		BronKerbosch(NodeSet P, NodeSet R, NodeSet X, Graph graph);
// 	private:
// 		Node pivot;
// 		NodeSet pivot_nbrs;
// 		Graph graph;
// 		Node findPivot(NodeSet PuX, NodeSet P, graph);
// 		def findNbrs(Node v, NodeSet S, graph);
// }
NodeSet getUnion(NodeSet& a, NodeSet& b){
  NodeSet result = a;
  result.insert(b.begin(), b.end());
  return result;
}
NodeSet getIntersection(const NodeSet& a, const NodeSet& b){
	NodeSet result;
	set_intersection(a.begin(),a.end(),b.begin(),b.end(),
                  std::inserter(result,result.begin()));
	return result;
}
NodeSet getDifference(const NodeSet& a, const NodeSet& b){
	NodeSet result;
	set_difference(a.begin(),a.end(),b.begin(),b.end(),
                  std::inserter(result,result.begin()));
	return result;
}
NodeSet findNbrs(Node v, NodeSet S, Graph graph){
	return getIntersection(graph[v],S);
}

Node findPivot(NodeSet PuX, NodeSet P, Graph graph){
	Node pivot = -1;
	NodeSet pivot_nbrs = NodeSet();
	for(auto it=PuX.begin(); it!=PuX.end();++it){
		auto v_nbrs = findNbrs((*it),P,graph);
		if(v_nbrs.size()>=pivot_nbrs.size()){
			pivot= (*it);
			pivot_nbrs = v_nbrs;
		}
	}
	return pivot;
}

void BronKerbosch(NodeSet P, NodeSet R, NodeSet X, Graph graph){

	if(P.size()==0 && X.size()==0){
		if(R.size()>maximum_clique.size()){
			maximum_clique = R;
		}
	}
	Node pivot;
	NodeSet pivot_nbrs;
	NodeSet clique;

	pivot = findPivot(getUnion(P,X), P, graph);
	pivot_nbrs = findNbrs(pivot, P, graph);
	// cout<<"Pivot"<<pivot<<endl;
	
	auto not_pivot_nbrs = getDifference(P, pivot_nbrs);
	for(auto it=not_pivot_nbrs.begin(); it!=not_pivot_nbrs.end();++it) {
		auto v_nbrs = findNbrs((*it),P,graph);
		NodeSet tmp = R;
		tmp.insert(*it);
		BronKerbosch(getIntersection(P,v_nbrs),tmp, getIntersection(X,v_nbrs), graph);
		P.erase(*it);
		X.insert(*it);
	}
}
static void alarm_handler(int sig){
	//Output Data
    ofstream of;
    of.open(output_file);

    for(auto const&element: maximum_clique){
        of << element <<  endl;
    }
    of.close();
}
int main(int argc, char* argv[]){
	struct sigaction act;
	act.sa_handler = alarm_handler;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;

	sigaction(SIGALRM, &act, 0);
    alarm(179);

	input_file = argv[1];
	output_file = argv[2];
	string line;

	Graph graph;
	Node v1;
	Node v2;

	cout<<"input_file:"<<input_file<<" output_file:"<<output_file<<endl;
	freopen(input_file.c_str(), "r", stdin);
	while(!getline(cin,line).eof()){
		istringstream ssline(line);
		string number;
		getline(ssline, number, ' ');
		v1 = atoi(number.c_str());
		getline(ssline, number, ' ');
		v2 = atoi(number.c_str());
		// cout<<"v1:"<<v1<<" v2:"<<v2<<endl;
		
		if(graph.count(v1)>0){
			graph[v1].insert(v2);
		}else{
			graph[v1]=NodeSet();
			graph[v1].insert(v2);
		}

		if(graph.count(v2)>0){
			graph[v2].insert(v1);
		}else{
			graph[v2]=NodeSet();
			graph[v2].insert(v1);
		}
	}

	NodeSet R = NodeSet();
	NodeSet P = NodeSet();
	NodeSet X = NodeSet();
	for (auto const& element : graph) {
    	P.insert(element.first);
  	}
  	cout<<"Node number: "<<P.size()<<endl;
	BronKerbosch(P,R,X,graph);
	cout<<"maximum_clique size:"<<maximum_clique.size()<<endl;

	
    return 0;
}