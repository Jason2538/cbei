m =[[int(i)  for i in input().split()] for i in range(9)]

ans = m[0][0]

x=0
y=0

for i in range(9):
    for j in range(9):
        if ans < m[i][j]:
            ans = m[i][j]
            x = j
            y = i
print(ans)
print(y+1, x+1)
           