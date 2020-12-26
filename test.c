int consistent(int current){
  int i;
  for(i=1; i < current; i++){
    if(check(current, i) == 0){
      max_check[current] = max(max_check[current], i);
      return 0;
    }
  }
  max_check[current] = current -1;
  return 1;
}

int BJ(int current){
  int i, jump;
  if(current > N){
    solution();
    return N;
  }
  max_check[current] = 0;
  for(i=0;i< K; i++){
    v[current] = i;
    if(consistent(current)){
      jump = BJ(current + 1);
      if(jump != current){
        return jump;
      }
    }
  }
  return max_check[current];
}
