vec4 mainFileFunction(vec4 v) {
	return -v;
}
void main() {
	headerOut = headerFunction(mainFileFunction(headerUboItem));
}
