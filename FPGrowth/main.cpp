#include <iostream>
#include <cstdio>
#include <sstream>
#include <vector>
#include <map>
#include <set>
#include <cstring>
#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>

using namespace std;
using PAIR = pair<int, int>;
using Item = int;
using Frequency = int;
using Pattern = string;
using FrequentPattern = pair<vector<Item>, Frequency>;
using ConditionalPatternBase = pair<vector<Item>, Frequency>;

struct FPNode{
    Item item;
    Frequency frequency;
    FPNode *parent;
    vector<FPNode *> children;
    FPNode *headerTableNodeLink;
    bool isroot;
    FPNode(){
        isroot = true;
        item = -1;
        frequency = -1;
        parent = NULL;
    };
    FPNode(Item i, FPNode *p){
        isroot = false;
        item = i;
        parent = p;
        frequency = 1;
        headerTableNodeLink = NULL;
    }
    FPNode(Item i, FPNode *p, Frequency f){
        isroot = false;
        item = i;
        parent = p;
        frequency = f;
        headerTableNodeLink = NULL;
    }
};
using HeaderTable = map<Item, pair<Frequency, FPNode *>>;
using SortedHeaderTableByFrequency = vector<pair<Item, pair<Frequency, FPNode *>>>;
class FPTree{
public:
    FPTree();
    FPTree(float min_support);
    FPTree(float min_support, vector<PAIR> flist_vec);
    void insertTransaction(vector<Item> transaction);
    void insertConditionPatternBase(ConditionalPatternBase pattern_base);
    void sortHeaderTableByFrequency();
    void preorder_print();
    void preorder_print(FPNode *node); 
    void headerTable_print();   
    bool empty();
    bool containSinglePath();
    set<FrequentPattern> FP_Growth();                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

private:
    FPNode *root;
    HeaderTable headerTable;
    SortedHeaderTableByFrequency sortedHeaderTableByFrequency;
    float min_support;
    vector<PAIR> flist_vec;
};

FPTree::FPTree(float support, vector<PAIR> FList_vec){
    root = new FPNode();

    min_support = support;
    flist_vec = FList_vec;
}
void FPTree::insertTransaction(vector<Item> transaction){
    // cout << "insert transaction "<<endl;
    // for(auto const& value: transaction) {
    //     cout << value << ',';
    // }
    // cout << endl;
    FPNode* p = root;
    Item item;
    for(int i=0; i<flist_vec.size(); i++){
        item = flist_vec[i].first;
        // cout << "check item "<<item<<endl;
        if(find(transaction.begin(), transaction.end(), item) != transaction.end()){ // transaction has item
            auto is_child = find_if(p->children.begin(),p->children.end(), 
                [item](FPNode* node){ return node->item == item;});
            if(is_child!=p->children.end()){ //is child
                // cout << item << " is a child of "<< p->item <<endl;
                p = *is_child;
                p->frequency+=1;
            }else{ //not a child
                // cout << item << " is not a child of "<<p->item<<endl;
                FPNode* newchild = new FPNode(item, p);
                p->children.push_back(newchild);
                if(headerTable.count(item)){
                    FPNode* ptr_table_item = headerTable[item].second;
                    while(ptr_table_item->headerTableNodeLink){
                        ptr_table_item = ptr_table_item->headerTableNodeLink;
                    }
                    ptr_table_item->headerTableNodeLink = newchild;
                }else{
                    headerTable[item].second = newchild;
                }
                p = newchild;
            }
        }
    }
}
void FPTree::insertConditionPatternBase(ConditionalPatternBase pattern_base){
    FPNode* p = root;
    auto items = pattern_base.first;
    auto frequency = pattern_base.second;
    Item item;
    for(int i=0; i<flist_vec.size(); i++){
        item = flist_vec[i].first;
        if(find(items.begin(), items.end(), item) != items.end() ){
            auto is_child = find_if(p->children.begin(), p->children.end(),
                [item](FPNode* node){ return node->item == item;});
            if(is_child!=p->children.end()){ //is child
                // cout << item << " is a child of "<< p->item <<endl;
                p = *is_child;
                p->frequency+=frequency;
            }else{ //not a child
                // cout << item << " is not a child of "<<p->item<<endl;
                FPNode* newchild = new FPNode(item, p, frequency);
                p->children.push_back(newchild);
                if(headerTable.count(item)){
                    FPNode* ptr_table_item = headerTable[item].second;
                    while(ptr_table_item->headerTableNodeLink){
                        ptr_table_item = ptr_table_item->headerTableNodeLink;
                    }
                    ptr_table_item->headerTableNodeLink = newchild;
                }else{
                    headerTable[item].second = newchild;
                }
                p = newchild;
            }
        }
    }
}
void FPTree::preorder_print(){
    cout << "Preoder Print FPTree\n";
    preorder_print(root);
}
void FPTree::preorder_print(FPNode* node){
    if(node!=NULL){
        cout << "Item: " << node->item << " Frequency: "<< node->frequency << endl;
        vector<FPNode *> children = node->children;
        for (int i=0; i<children.size(); i++){
            preorder_print(children[i]);
        }
    }
}
void FPTree::headerTable_print(){
    cout << "FPTree header table size: "<< headerTable.size()<< endl;
}
bool compare_by_value(pair<Item, pair<Frequency, FPNode *>> &lhs, pair<Item, pair<Frequency, FPNode *>> &rhs){
    return (lhs.second.first > rhs.second.first);
}
bool cmp_by_value(const PAIR& lhs, const PAIR& rhs) {  
  return lhs.second > rhs.second; 
}
// bool compare_by_value(pair<Pattern, Frequency> &lhs, pair<Pattern, Frequency> &rhs){
//     return (lhs.first < rhs.first);
// }
void FPTree:: sortHeaderTableByFrequency(){
    for( HeaderTable::iterator it = headerTable.begin(); it != headerTable.end(); ++it )
    {
      Item key = it->first;
      pair<Frequency, FPNode *> value = it->second;
      int frequency = 0; //initialize frequency
      FPNode* ptr = value.second;
      while(ptr!=NULL){
        frequency += ptr->frequency;
        ptr = ptr->headerTableNodeLink;
      }
      it->second.first = frequency;
    }
    // for(HeaderTable::iterator it=headerTable.begin(); it!=headerTable.end(); ++it){
    //     cout << "Item: "<<it->first << " Frequency: " <<it->second.first << endl;
    // }
    sortedHeaderTableByFrequency.assign(headerTable.begin(), headerTable.end());
    sort(sortedHeaderTableByFrequency.begin(), sortedHeaderTableByFrequency.end(), compare_by_value);

    // cout << "sortHeaderTableByFrequency: Finish\n sortedHeaderTableByFrequency value: \n";
    // for(SortedHeaderTableByFrequency::iterator it=sortedHeaderTableByFrequency.begin(); it!=sortedHeaderTableByFrequency.end(); ++it){
    //     cout << "Item: "<<it->first << " Frequency: " <<it->second.first << endl;
    // }
}
bool FPTree::containSinglePath(){
    // cout << "check single path\n";
    FPNode* ptr = root;
    while(ptr!=NULL){
        if(ptr->children.size()>1){
            return false;
        }
        if(ptr->children.size()==0)break;
        else ptr = ptr->children[0];
    }
    return true;
}
bool FPTree::empty(){
    // cout << "check empty\n";
    return root->children.size()==0;
}
void pattern_print(pair<Pattern, Frequency>pattern){
    cout << "Pattern: " << pattern.first;
    // for(auto it=pattern.first.begin(); it!=pattern.first.end(); it++){
    //     cout<< (*it) << ' ';
    // }
    cout << " Frequency: " << pattern.second << endl;
}

set<FrequentPattern> FPTree::FP_Growth(){
    if(empty()){return {};}
    if(containSinglePath()){ //FPTree only contains a single path (no branch)
        //Find Combinition of notes in the single path as frequent patters
        // cout << "Is single path\n";
        set<FrequentPattern> return_frequent_patterns;
        FPNode *ptr = root->children[0];
        while(ptr!=NULL){
            set<FrequentPattern> new_frequent_patters_set;
            for(set<FrequentPattern>::iterator it = return_frequent_patterns.begin(); it != return_frequent_patterns.end(); ++it){
                FrequentPattern pattern = *it;
                pattern.first.push_back(ptr->item);
                pattern.second = ptr->frequency;
                new_frequent_patters_set.insert(pattern);
            }
            return_frequent_patterns.insert(new_frequent_patters_set.begin(),new_frequent_patters_set.end());
            
            FrequentPattern newPattern;
            newPattern.first.push_back(ptr->item);
            newPattern.second = ptr->frequency;
            return_frequent_patterns.insert(newPattern);

            if(ptr->children.size()==0)break;
            
            else ptr = ptr->children[0];
        }
        return return_frequent_patterns;
    }
    else{
        //Sort Header Table by Item Frequency
        sortHeaderTableByFrequency();
        auto table = sortedHeaderTableByFrequency;
        set<FrequentPattern> return_frequent_patterns;
        
        //For every item in header table...
        for (int i=table.size()-1; i>=0; i--){
            Item condition_item = table[i].first;
            Frequency condition_frequency = table[i].second.first;
            //Add the condition pattern
            FrequentPattern newPattern;
            newPattern.first.push_back(condition_item);
            newPattern.second = condition_frequency;
            return_frequent_patterns.insert(newPattern);

            //Find Conditional Pattern Base
            map<Item, Frequency> FList; //update FList for building conditional FP-tree
            set<ConditionalPatternBase> conditional_pattern_bases;
            FPNode *ptr_horizontal = table[i].second.second;

            // cout << "Conditional item: " << condition_item << endl;
            while(ptr_horizontal!=NULL){ //traverse by headerTableNodeLink               
                ConditionalPatternBase pattern_base;
                pattern_base.second = ptr_horizontal->frequency;
                FPNode *ptr_vertical = ptr_horizontal->parent;

                while(!ptr_vertical->isroot){
                    pattern_base.first.insert(pattern_base.first.begin(),ptr_vertical->item);
                    

                    if(FList.count(ptr_vertical->item)>0){
                        FList[ptr_vertical->item] += ptr_horizontal->frequency;
                    }else{
                        FList[ptr_vertical->item] = ptr_horizontal->frequency;
                    }

                    ptr_vertical = ptr_vertical->parent;
                }
                conditional_pattern_bases.insert(pattern_base);
                ptr_horizontal = ptr_horizontal->headerTableNodeLink;
            }
            // Sort FList by item count, output: FList_vec
            vector<PAIR> FList_vec(FList.begin(), FList.end());
            sort(FList_vec.begin(), FList_vec.end(), cmp_by_value);
            for (int i = 0; i < FList_vec.size(); i++) {  
                if(FList_vec[i].second < min_support){
                    FList_vec.erase(FList_vec.begin()+i, FList_vec.end());
                    break;
                }
            }
            //Build conditional FP-tree
            FPTree conditional_fptree = FPTree(min_support, FList_vec);
            for(set<ConditionalPatternBase>::iterator it=conditional_pattern_bases.begin(); it != conditional_pattern_bases.end(); ++it){
                ConditionalPatternBase pattern_base = *it;
                conditional_fptree.insertConditionPatternBase(pattern_base);
            }
            //conditional_fptree.preorder_print();
            //Recursion
            set<FrequentPattern>conditional_frequent_patterns = conditional_fptree.FP_Growth();
            
            
            for(auto it = conditional_frequent_patterns.begin(); it!=conditional_frequent_patterns.end(); it++){
                FrequentPattern pattern = *it;
                return_frequent_patterns.insert(pattern);
                
                //Add prefix to conditional frequent pattern
                pattern.first.push_back(condition_item);

                //insert to result
                return_frequent_patterns.insert(pattern);

            }
        }
        return return_frequent_patterns;
    }
}

Pattern vec_to_string(vector<Item> vec){
    std::ostringstream oss;
    if (!vec.empty()){
        // Convert all but the last element to avoid a trailing ","
        std::copy(vec.begin(), vec.end()-1,
            std::ostream_iterator<int>(oss, ","));

        // Now add the last element with no delimiter
        oss << vec.back();
    }
    return oss.str();
}
vector<Item> string_to_vec(Pattern pattern){
    vector<Item> output;
    istringstream ss(pattern);
    string token;
    while(getline(ss,token,',')){
        Item item = atoi(token.c_str());
        output.push_back(item);
    }
    return output;
}
bool compare_by_pattern(pair<Pattern, Frequency> &lhs, pair<Pattern, Frequency> &rhs){
    vector<Item> lv = string_to_vec(lhs.first);
    vector<Item> rv = string_to_vec(rhs.first);
    if (lv.size() < rv.size()) return true;
    else if (lv.size() > rv.size()) return false;
    else return lv < rv;
}
int main(int argc, char* argv[])
{
    float min_support_percent;
    string input_file;
    string output_file;
    
    min_support_percent = atof(argv[1]);
    input_file = argv[2];
    output_file = argv[3];
    //cout << "min_support: " << min_support_percent << " input_file " << input_file << " output_file " << output_file;
    // Input Data and Build FList
    freopen(input_file.c_str (), "r", stdin);
    vector<vector<Item> > transactions;
    string line;
    map<Item, Frequency> FList;

    while(!getline(cin,line).eof()){
    	vector<int> arr;
    	istringstream ssline(line);
    	string number;
    	while(getline(ssline, number,',')){
            int item = atoi(number.c_str());
    		arr.push_back(item);

            if(FList.count(item)>0){
                FList[item] += 1;
            }else{
                FList[item] = 1;
            }
    	}
    	transactions.push_back(arr);
    }
    float min_support = min_support_percent * transactions.size();
    // Build FList
    // std::map<int, int> FList;
    // for(int i=0; i<transactions.size(); i++){
    //     for(int j=0; j<transactions[i].size(); j++){
    //         int item;
    //         item = transactions[i][j];
    //         if(FList.count(item)>0){
    //             FList[item] += 1;
    //         }else{
    //             FList[item] = 1;
    //         }
    //     }
    // }
    // cout << "FList size is "<< FList.size() << "\n";

    // Sort FList by item count, output: FList_vec
    vector<PAIR> FList_vec(FList.begin(), FList.end());
    sort(FList_vec.begin(), FList_vec.end(), cmp_by_value); 
        // for (int i = 0; i < FList_vec.size(); i++) {  
        //     cout << FList_vec[i].first <<": "<<FList_vec[i].second << endl;
        // }
    for (int i = 0; i < FList_vec.size(); i++) {  
        if(FList_vec[i].second < min_support){
            FList_vec.erase(FList_vec.begin()+i, FList_vec.end());
            break;
        }
    }
    // for (int i = 0; i < FList_vec.size(); i++) {  
    //     cout << FList_vec[i].first <<": "<<FList_vec[i].second << endl;
    // }
    FPTree fptree(min_support, FList_vec);
    for(int i=0; i<transactions.size(); i++){
        fptree.insertTransaction(transactions[i]);
    }
    //fptree.sortHeaderTableByFrequency();
    set<FrequentPattern> frequent_patterns = fptree.FP_Growth();

    map<Pattern, Frequency> output_frequent_patterns;
    for(auto it=frequent_patterns.begin(); it!=frequent_patterns.end(); it++){
        auto items = (*it).first;
        sort(items.begin(), items.end());
        Pattern pattern = vec_to_string(items);

        //cout << pattern << ":" << setprecision(4) << fixed << (double)(*it).second/(double)transactions.size() << endl;

        if(output_frequent_patterns.count(pattern)>0){
            if(output_frequent_patterns[pattern] < (*it).second)output_frequent_patterns[pattern] = (*it).second;
        }else output_frequent_patterns[pattern] = (*it).second;
    }
    //Output Data
    ofstream of;
    of.open(output_file);
    of << setprecision(4) << fixed;

    vector<pair<Pattern, Frequency>> sorted_output_frequent_patterns (output_frequent_patterns.begin(), output_frequent_patterns.end());
    sort(sorted_output_frequent_patterns.begin(), sorted_output_frequent_patterns.end(), compare_by_pattern);


    for(auto it=sorted_output_frequent_patterns.begin(); it!=sorted_output_frequent_patterns.end(); it++){
        of << (*it).first << ":" <<(double)(*it).second/(double)transactions.size() << endl;
    }
    of.close();
    return 0;
}
