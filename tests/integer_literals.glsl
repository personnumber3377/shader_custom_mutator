precision mediump float;
precision mediump int;

void main() {
    int main_uninitialized_int;
    int main_initialized_int = 42;
    int main_uninitialized_uint;
    int main_initialized_uint_no_suffix = 42;
    int main_initialized_uint_suffix = 42;
    int main_hex_no_suffix_upper = 0xFF;
    int main_hex_suffix_upper = 0xFF;
    int main_hex_no_suffix_lower = 0xff;
    int main_hex_suffix_lower = 0xff;
    int main_hex_no_suffix_mixed = 0xFf;
    int main_hex_suffix_mixed = 0xFf;
    int main_negative = -1;
    int main_octal = 0777;
}
