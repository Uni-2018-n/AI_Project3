int consistent( int current){
  int j, a;
  int old=0, del =0;
  for(j = current + 1; j <= N; j++){
    for(a= 0; a< K; a++){
      if(domains[j][a] == 0){
        old++;
        v[j] = a;
        if( check(current, j) == 0){ // im here
          domains[j][a] = current;
          del++;
        }
      }
    }
    if(del){
      checking[current][j] = 1;
    }
    if(old - del ==0){
      return j;
    }
  }
  return 0;
}

void restore(int i){
  int j, a;
  for(j=i+1; j <= N; j++){
    if(checking[i][j]){
      checking[i][j] =0;
      for(a =0;a< K; a++){
        if(domains[j][a] == i){
          domains[j][a] = 0;
        }
      }
    }
  }
}


int FC_CBJ(int z){
  int h, i, j, jump, fail;

  if(z > N){
    solution();
    return(N);
  }
  empty(conf_set[i]);
  for(i=0; i < K; i++){
    if(domains[z][i]){
      continue;
    }
    v[z] = i;
    fail = consistent(z);
    if(fail == 0){
      jump = FC_CBJ(z + 1);
      if(jump != z){
        return jump;
      }
    }
    restore(z);
    if(fail){
      for(j=1; j < z; j++){
        if(checking[j][fail]){
          add(j, conf_set[z]);
        }
      }
    }
  }

  for( j =1; j < z; j++){
    if(checking[j][z]){
      add(j, conf_set[z])
    }
  }
  h= max(conf_set[z]);
  merge(conf_set[h], conf_set[z]);
  for(i = z; i>= h; i++){
    restore(i);
  }
  return h;
}
