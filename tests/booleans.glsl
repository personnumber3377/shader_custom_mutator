precision mediump float;
precision mediump int;

void main() {
    bool main_uninitialized;
    bool main_true_initialized = true;
    bool main_false_initialized = false;
    bool main_assign;
    main_assign = main_true_initialized;
    main_assign = main_false_initialized;
    main_assign = true;
    main_assign = false;
}
