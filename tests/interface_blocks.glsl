#version 310 es

precision mediump float;
precision mediump int;

in input_block { float y; };
out output_block { float z; };
buffer buffer_block { float w; };

in input_block { float y; } input_data;
out output_block { float z; } output_data;
buffer buffer_block { float w; } buffer_data;
