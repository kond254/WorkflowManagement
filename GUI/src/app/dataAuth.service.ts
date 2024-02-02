import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { mergeMap } from 'rxjs/operators';
import { HashService} from './hash.service';
import { from } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataAuthService {
  private usersDataJson = 'assets/userData.json';
  
   constructor(private http: HttpClient, private hashService: HashService) {}

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(this.usersDataJson);
  }

  checkCredentials(username: string, password: string): Observable<string> {
    return from(this.hashService.hashPassword(password)).pipe(
      mergeMap((hashedPassword) => {
        return this.getUsers().pipe(
          map((users) => {
            const user = users.find((u) => u.username == username && u.password == hashedPassword);
            if (users.some((u) => u.username == username && u.password == hashedPassword)) {
              return user.role;
            } else if (users.some((u) => u.username == username && u.password != hashedPassword)) {
              return 'invalidPassword';
            } else {
              return 'invalidUsername';
            }
          })
        );
      })
    );
  }
}