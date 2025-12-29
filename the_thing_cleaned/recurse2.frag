void cfoo(float);
float cbar(int)
{
	cfoo(4.2);
	return 3.2;
}
void CA();
void CC();
void CB() { CC(); }
void CD() { CA(); }
void CAT();
void CCT();
void CBT() { CCT(); CCT(); CCT(); }
void CDT() { CAT(); }
