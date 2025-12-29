bool compare_uint8_t  (highp uint a, highp uint b)    { return a == b; }
void main (void)
{
	bool allOk = true;
	allOk = allOk && compare_uint8_t(uint(block.var), 7u);
	if (allOk)
		ac_numPassed++;
	block.var = uint8_t(9u);
}
