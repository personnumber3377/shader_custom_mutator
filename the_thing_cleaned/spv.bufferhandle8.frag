struct Blah {
    T1 t1;
    T2 t2;
};
layout(set=0, binding=0) buffer T3 {
  Blah Bindings[];
} t3;
void main() {
    Blah x = t3.Bindings[2];
    t3.Bindings[0] = t3.Bindings[1];
}
