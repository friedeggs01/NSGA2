#include <bits/stdc++.h>
using namespace std;

#define INF 1e9
#define OBJ_CNT 3
#define N 7
#define ETA_C 15
#define ETA_M 20
#define POP_SIZE 100
#define MAX_GENERATION 300
#define CROSSOVER_RATE 0.9
#define MUTATION_RATE 0.14
#define K 5


double random_double() {
    return 1.0 * rand() / RAND_MAX;
}
double random() {
    return 1.0 * rand() / RAND_MAX;
}
// Class biểu diễn một cá thể
class Individual {
public:
    int dim;                    // Chiều dài chuỗi gen của cá thể
    int num_objectives;         // Số hàm mục tiêu

    double x[N];  // Chuỗi gen biểu diễn đồ vật được chọn
    double fitness[OBJ_CNT] = {INF};    // Giá trị hàm thích nghi

    Individual() {
        this->dim = N;
        this->num_objectives = OBJ_CNT;
    }

    Individual(const Individual &p) {
        this->dim = p.dim;
        this->num_objectives = p.num_objectives;
        for (int i=0; i<p.dim; i++)
            this->x[i] = p.x[i];
        for (int i=0; i<num_objectives; i++)
            this->fitness[i] = p.fitness[i];
    }

    void random_init() {
        for (int i=0; i<dim; i++){
            x[i] = random();
        }
    }
    void evaluate() {
        double temp = 0;
        for(int i=0; i<N; i++){
            x[i] = max(0.0, min(x[i], 1.0));
        }
        for(int i=2; i<N; i++){
            temp += ((x[i]-0.5)*(x[i]-0.5)) - cos(20*M_PI*(x[i] - 0.5));
        }
        double g = 100*(K + temp);
        fitness[0] = 0.5*x[0]*x[1]*(1+g);
        fitness[1] = 0.5*x[0]*(1-x[1])*(1+g);
        fitness[2] = 0.5*(1-x[0])*(1+g);
    }

    /*void evaluate() {
        double f[OBJ_CNT];
        double temp = 0;
        for(int i=2; i<N; i++){
            temp += ((x[i]-0.5)*(x[i]-0.5)) - cos(20*M_PI*(x[i] - 0.5));
        }
        double g = 100*(K + temp);
        for(int i=0; i<num_objectives; i++){
            x[i] = max(0.0, min(x[i], 1.0));
            if(i==0){
                f[i] = 0.5*(1+g); 
            } else {
                f[i] = 0.5*(1-x[num_objectives-1-i])*(1+g);
            }
            for(int j=0; j<(num_objectives-1); j++){
             if(j<(num_objectives-1-i)){
                f[i] *= x[j];
             } 
            }
            fitness[i] = f[i];
        }
    }*/


    bool dominate(Individual& other) {
        bool superior = false;
        for (int i=0; i<num_objectives; i++)
            if (this->fitness[i] > other.fitness[i])
                return false;
            else if (this->fitness[i] < other.fitness[i])
                superior = true;
        return superior;
    }
    
    static vector<Individual> SBX(Individual& p1, Individual& p2) {
        double EPSILON = 1E-6;
        double UB = 1.0;
        double LB = 0.0; 

        int dim = p1.dim;
        Individual o1, o2;

        for (int i=0; i<dim; i++) {
            if (random_double() && abs(p1.x[i] - p2.x[i]) >= EPSILON) {
                double y1 = min(p1.x[i], p2.x[i]);
                double y2 = max(p1.x[i], p2.x[i]);

                double rand_num = random_double();

                // calculate 1st offspring
                double beta = 1.0 + (2.0 * (y1 - LB) / (y2 - y1));
                double alpha = 2.0 - pow(beta, -(ETA_C + 1.0));
                double betaq;
                
                if (rand_num <= (1.0 / alpha)) {
                    betaq = pow(rand_num * alpha, 1.0 / (ETA_C + 1.0));
                } else {
                    betaq = pow(1.0 / (2.0 - rand_num * alpha), 1.0 / (ETA_C + 1.0));
                }

                o1.x[i] = 0.5 * ((y1 + y2) - betaq * (y2 - y1));
                o1.x[i] = max(LB, min(UB, o1.x[i]));

                // calculate 2nd offspring
                beta = 1.0 + (2.0 * (UB - y2) / (y2 - y1)); 
                alpha = 2.0 - pow(beta, -(ETA_C + 1.0));
                
                if (rand_num <= (1.0/alpha)) {
                    betaq = pow(rand_num * alpha, 1.0 / (ETA_C + 1.0));
                } else {
                    betaq = pow(1.0 / (2.0 - rand_num * alpha), 1.0/(ETA_C + 1.0));
                }
                
                o2.x[i] = 0.5 * ((y1 + y2) + betaq * (y2 - y1));
                o2.x[i] = max(LB, min(UB, o2.x[i]));
            } else {
                o1.x[i] = p1.x[i];
                o2.x[i] = p2.x[i];
            }
        }

        vector<Individual> offspring;
        offspring.push_back(o1);
        offspring.push_back(o2);

        return offspring;
    }

    void PM() {
        double UB = 1;
        double LB = 0;
        
        double mut_prob = 1.0 / dim;
        for (int i=0; i<dim; i++) {
            if (random_double() < mut_prob) {
                double delta1 = (x[i] - LB) / (UB - LB);
                double delta2 = (UB - x[i]) / (UB - LB);

                double rand_num = random_double();
                double mut_pow = 1.0 / (ETA_M + 1.0);

                double deltaq;
                if (rand_num <= 0.5) {
                    double val = 2.0 * rand_num + (1.0 - 2.0 * rand_num) * (pow(1.0 - delta1, ETA_M + 1.0));
                    double deltaq = pow(val, mut_pow) - 1.0;
                } else {
                    double val = 2.0 * (1.0 - rand_num) + 2.0 * (rand_num - 0.5) * (pow(1.0 - delta2, ETA_M + 1.0));
                    double deltaq = 1.0 - pow(val, mut_pow);
                }

                x[i] = x[i] + deltaq * (UB - LB);
                x[i] = max(LB, min(UB, x[i]));
            }
        }
    }
};


class NSGAIISelection {
public:
    static bool is_pareto_point(Individual p, vector<Individual>& pop) {
        for (Individual& indiv: pop)
            if (indiv.dominate(p))
                return false;
        return true;
    }

    static void select(vector<Individual>& pop, int count) {
        vector<Individual> new_pop;

        while (new_pop.size() < count) {
            vector<Individual> pareto;
            vector<Individual> non_pareto;

            for (Individual& p: pop)
                if (is_pareto_point(p, pop))
                    pareto.push_back(p);
                else
                    non_pareto.push_back(p);
            pop = move(non_pareto);

            if (new_pop.size() + pareto.size() > count) {
                sort_by_crowding_distance(pareto);
                pareto.resize(count - new_pop.size());
            }
            new_pop.insert(new_pop.end(), pareto.begin(), pareto.end());
        }

        pop = move(new_pop);
    }

    class ObjectiveComparator {
    public:
        int obj_idx;
        vector<Individual> pop;
        ObjectiveComparator(vector<Individual>& pop) {
            this->pop = pop;
        }

        bool operator()(const int& i1, const int& i2) {
            return pop.at(i1).fitness[obj_idx] < pop.at(i2).fitness[obj_idx];
        }
    };

    static void sort_by_crowding_distance(vector<Individual>& pop) {
        int PS = pop.size(); // kích cỡ của quần thể
        int obj_cnt = pop.at(0).num_objectives; // truy cập phần tử đầu tiên trong quần thể để xác định hàm mục tiêu
        vector<int> indices; //chỉ số để đánh số từng cá thể trong quần thể
        double I[PS]; //khoảng cách crowding distance 

        for (int i=0; i<PS; i++) {
            indices.push_back(i); // indices={0,1,2,...,PS-1}
            I[i] = 0.0;
        }

        ObjectiveComparator cmp(pop);
        for (int k=0; k<obj_cnt; k++) {
            cmp.obj_idx = k; // xác định hàm mục tiêu đang xét là hàm mục tiêu thứ k+1 
            sort(indices.begin(), indices.end(), cmp); // sắp xếp từ bé tới lớn tại cùng một hàm fitness thứ k+1 

            I[indices.at(0)] = I[indices.at(PS-1)] = INF; // gán cho đầu cuối bằng vô cùng
            double range = pop.at(indices.at(PS-1)).fitness[k]
            - pop.at(indices.at(0)).fitness[k]; // kiểu xác định range để chuẩn hóa

            for (int i=1; i<PS-1; i++) {
                if (I[indices.at(i)] == INF)
                    continue;
                I[indices.at(i)] += (pop.at(indices.at(i+1)).fitness[k] -
                                     pop.at(indices.at(i-1)).fitness[k]) / range;
            }
        }

        sort(indices.begin(), indices.end(), [&](int ia, int ib) { return I[ia] > I[ib]; }); // lấy những điểm có khoảng cách xa vì nếu khoảng cách gần thì có thể có lời giải tương đồng 
        vector<Individual> old_pop = move(pop);
        pop.clear();
        for (int i: indices)
            pop.push_back(old_pop.at(i));
    }
};


class Population {
public:
    vector<Individual> population;

    void init() {
        for (int i=0; i<POP_SIZE; i++) {
            Individual p;
            p.random_init();
            p.evaluate();
            population.push_back(p);
        }
    }

    // Sinh sản = lai ghép + đột biến
    void reproduction(int count) {
        vector<Individual> offspring;

        // lai ghép
        while (offspring.size() < count) {
            int i1 = rand() % POP_SIZE;
            int i2 = rand() % POP_SIZE;
            while (i2 == i1)
                i2 = rand() % POP_SIZE;

            Individual p1 = population[i1];
            Individual p2 = population[i2];
            if (random() < CROSSOVER_RATE) {
                vector<Individual> children = Individual::SBX(p1, p2);
                offspring.insert(offspring.end(), children.begin(), children.end());
            }
            else {
                offspring.push_back(Individual(p1));
                offspring.push_back(Individual(p2));
            }
        }
        while (offspring.size() > count)
            offspring.pop_back();

        // đột biến
        for (Individual &indiv: offspring)
            if (random() < MUTATION_RATE)
                indiv.PM();

        population.insert(population.end(), offspring.begin(), offspring.end());
    }

    // Chọn lọc theo NSGA-II
    void natural_selection(int count) {
        NSGAIISelection::select(population, count);
    }
};

int main() {
    srand ( time(NULL) );

    /*=== Thuật toán NSGA-II ===*/
    // Khởi tạo quần thể
    Population pop;
    pop.init();
    cout << "Generation 0" << endl;
    for (Individual p: pop.population){
        for(int i=0; i<OBJ_CNT; i++) {
            cout <<p.fitness[i];
            if(i<OBJ_CNT-1){
                cout << ", ";
            }
        }
        cout << ")" <<endl;
    }
    for (Individual p: pop.population){
        for(int i=0; i<OBJ_CNT; i++) {
            cout <<p.fitness[i];
            if(i<OBJ_CNT-1){
                cout << " ";
            }
        }
        cout <<endl;
    }
    // vòng lặp tiến hóa
    for (int t=1; t<=MAX_GENERATION; t++) {
        // sinh sản
        pop.reproduction(POP_SIZE);

        // đánh giá cá thể
        for (Individual &indiv: pop.population)
            indiv.evaluate();

        // chọn lọc tự nhiên
        pop.natural_selection(POP_SIZE);

        // in kết quả mỗi thế hệ
        cout << "Generation " << t << endl;
    }

    /*=== In kết quả cuối ===*/
    //cout << "===========" << endl;
    cout << "FINAL RESULT:" << endl;
    for (Individual p: pop.population){
        for(int i=0; i<OBJ_CNT; i++) {
            cout <<p.fitness[i];
            if(i<OBJ_CNT-1){
                cout << ", ";
            }
        }
        cout << ")" <<endl;
    }
    for (Individual p: pop.population){
        for(int i=0; i<OBJ_CNT; i++) {
            cout <<p.fitness[i];
            if(i<OBJ_CNT-1){
                cout << " ";
            }
        }
        cout <<endl;
    }
    double sum=0;
    // for (Individual p: pop.population){
    //         sum+= pow((p.fitness[0]+p.fitness[1]+p.fitness[2]-0.5),2)/3;
    // }
    // cout << sqrt(sum)/POP_SIZE;
    for (Individual p: pop.population){
        
            sum+=pow(p.x[2]-0.5,2)+pow(p.x[3]-0.5,2)+pow(p.x[4]-0.5,2)+pow(p.x[5]-0.5,2)+pow(p.x[6]-0.5,2);
    }
    cout << sqrt(sum)/POP_SIZE;
}
