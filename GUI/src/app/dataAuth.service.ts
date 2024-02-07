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

//This class is used to compare the entered username and password with the stored user data in userData.json
export class DataAuthService {

  private usersDataJson;

  constructor(private http: HttpClient, private hashService: HashService) {
    this.usersDataJson= '/assets/userData.json';
  }
  //This method will be receive the specified username and password hash from the userData.json file
  getUsers(): Observable<any[]> {
    console.log(this.usersDataJson)
    return this.http.get<any[]>(this.usersDataJson);
  }

  //This method compares the user input from the login window with the user data from the userData.json file and returns the strings invalidPassword/invalidUsername
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