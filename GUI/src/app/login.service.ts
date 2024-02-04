import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

//This Class enables a boolean and string value of the logged in user to be exchanged between components
export class LoginService {
  private isLoggedIn: boolean = false;
  private userLoggedIn: string = '';

  //This method get the boolean value from the login (true/false)
  getloginValue(): boolean {
    return this.isLoggedIn;
  }

  //This method set the boolean value from the login (true/false)
  setloginValue(value: boolean): void {
    this.isLoggedIn = value;
  }

  //This method get the string value from the login (username)
  getloginUser(): string{
    return this.userLoggedIn;
  }

  //This method set the string value from the login (username)
  setloginUser(value: string): void {
    this.userLoggedIn = value;
  }
}