struct A {
	float x;
};
A test() {
	return A(1.0);
}
void main() {
	test().z;
}
