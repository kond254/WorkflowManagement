import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class DataAuthService {
  private usersDataJson = 'assets/userData.json';
  
   constructor(private http: HttpClient) {}

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(this.usersDataJson);
  }

  checkCredentials(username: string, password: string): Observable<string> {
    return this.getUsers().pipe(
      map((users) => {
        const user = users.find((u) => u.username == username && u.password == password);
        if (users.some((u) => u.username == username && u.password == password)) {
          return user.role;

        } else if (users.some((u) => u.username == username && u.password != password)) {
          return 'invalidPassword';

        } else {
          return 'invalidUsername';
        }
      })
    );
  }
}