double fitness(unsigned char* a, int n, unsigned char* b)
{
    int i, d;
    double f;

    f = 0;
    for (i = 0; i != n; ++i) {
        d = a[i] - b[i];
        f += d * d;
    }
    return f / n;
}
