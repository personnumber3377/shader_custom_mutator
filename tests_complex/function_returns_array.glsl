HEADER: frag 3 6

// Roundtrip a shader which has a function that returns an array...

#version 300 es

float[5] f() {
	return float[5](3.4, 4.2, 5.0, 5.2, 1.1);
}

void main() {
	float[5] x = f();
}