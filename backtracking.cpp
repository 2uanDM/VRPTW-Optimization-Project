#include<bits/stdc++.h>
using namespace std;
const long long maxN = 1e3+1;
int n,t0=0,e[maxN],l[maxN],d[maxN];
int c[maxN][maxN],t[maxN][maxN];

int res[maxN];
int mark[maxN];

int minn = 1e8;
void input()
{
    cin >> n;
    for(int i = 1; i <= n; ++i)
        cin >> e[i] >> l[i] >> d[i];
    int i = 0, j = 1, a,b;
    while(i <= n-1 && j <= n)
    {
        cin >> a >> b;
        c[i][j] = c[j][i] = a; t[i][j] = t[j][i] = b;
        j++;
        if (j > n)
        {
            i++;
            j = i+1;
        }
    }
}
void solution()
{
    int time_current = t0;
    int sum = 0; // tổng quảng đường di chuyển

    bool ok = true; //kiểm tra xem với solution này thì có đi hết từ đầu đến cuối được ko
    for(int i = 1; i<=n; ++i)
    {
        if (time_current + t[res[i-1]][res[i]] <= l[res[i]]) // nếu như thời gian hiện tại + thời gian để di chuyển đến i mà <= l[i]
            {
                sum = sum + c[res[i-1]][res[i]];

                time_current = time_current + t[res[i-1]][res[i]] + d[res[i]];
            }
        else
            return;
    }
    minn = min(minn, sum);
}
void print_lst()
{
    for(int i = 1; i<=n; ++i)
        cout << res[i] << " ";
    cout << endl;
}
void Try(int k)
{
    for (int i = 1; i<=n; ++i)
    {
        if (mark[i]==0) // Check đã đi qua hay chưa
            {
                res[k] = i; // Ghi nhận cấu hình
                mark[i] = 1; // Đã sử dụng phần tử này
                if (k == n)
                    solution();
                else
                    Try(k+1);
                mark[i] = 0;
            }
    }
}
int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    freopen("cc.inp","r",stdin);
    freopen("cc.out","w",stdout);

    input();
    Try(1);
    cout << minn;

}