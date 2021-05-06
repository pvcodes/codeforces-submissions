#include <bits/stdc++.h>
using namespace std;

typedef long long int ll;

#define test(t) \
    int t;      \
    cin >> t;   \
    while (t--)
#define f(i, a, b) for (int(i) = (a); (i) < (b); ++(i))
#define endl "\n"
#define deb(x) cout << #x << ": " << x << endl;
#define fast                          \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

void solve() {
    string A;
    cin >> A;
    int i = 0;
    int j = A.length() - 1;
    while (i < j) {
        if (A[i] == A[j]) {
            i++;
            j--;
        } else {
            if (i == 0 && A[j] == '0') {
                j--;
            } else {
                cout << "NO" << endl;
                return;
            }
        }
    }
    cout << "YES" << endl;
}
int main() {
    fast;
    // test(t)
    solve();
    return 0;
}
