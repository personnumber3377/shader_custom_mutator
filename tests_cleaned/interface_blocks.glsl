precision mediump float;
precision mediump int;

uniform uniform_block { float x; };
in input_block { float y; };
out output_block { float z; };
buffer buffer_block { float w; };
uniform uniform_block { float x; } uniform_data;
in input_block { float y; } input_data;
out output_block { float z; } output_data;
buffer buffer_block { float w; } buffer_data;
