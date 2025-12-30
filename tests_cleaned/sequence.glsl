precision mediump float;
precision mediump int;

void test() {
    1, 2, 3, 4;
    1, 2, (3, 4);
    1, (2, 3, 4);
    (1, 2), 3, 4;
    (1, 2, 3), 4;
    (1, 2, (3, 4));
    (1, (2, 3, 4));
    ((1, 2), 3, 4);
    ((1, 2, 3), 4);
}
