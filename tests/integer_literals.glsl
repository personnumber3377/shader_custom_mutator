precision mediump float;
precision mediump int;

void main() {
    int main_uninitialized_int;
    int main_initialized_int = 42;
    uint main_uninitialized_uint;
    uint main_initialized_uint_no_suffix = 42;
    uint main_initialized_uint_suffix = 42u;
    uint main_hex_no_suffix_upper = 0xFF;
    uint main_hex_suffix_upper = 0xFFu;
    uint main_hex_no_suffix_lower = 0xff;
    uint main_hex_suffix_lower = 0xffu;
    uint main_hex_no_suffix_mixed = 0xFf;
    uint main_hex_suffix_mixed = 0xFfU;
    int main_negative = -1;
    uint main_octal = 0777;
}
