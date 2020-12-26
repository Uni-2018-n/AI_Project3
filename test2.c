int consistent(int current){
  int i;
  for(i=1;i<current;i++){
    if(check(current, i) == 0){
      add(i, conf_set[current]);
      return 0;
    }
  }

  return 1;
}

int CBJ(int current){
  int h, i, jump;
  if(current > N){
    solution();
    return N;
  }
  empty(conf_set[current]);
  for(i=0;i<K;i++){
    v[current] = i;
    if(consistent(current)){
      jump = CBJ(current + 1);
      if(jump != current){
        return jump;
      }
    }
  }
  h = max(conf_set[current])
  merge(conf_set[h], conf_set[current])
  return h;
}
