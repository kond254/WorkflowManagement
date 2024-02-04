import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

//This Class enables a boolean and string value of the logged in user to be exchanged between components
export class LoginService {
  private isLoggedIn: boolean = false;
  private userLoggedIn: string = '';

  //Function to get the boolean value from the login (true/false)
  getloginValue(): boolean {
    return this.isLoggedIn;
  }

  //Function to set the boolean value from the login (true/false)
  setloginValue(value: boolean): void {
    this.isLoggedIn = value;
  }

  //Function to get the string value from the login (username)
  getloginUser(): string{
    return this.userLoggedIn;
  }

  //Function to set the string value from the login (username)
  setloginUser(value: string): void {
    this.userLoggedIn = value;
  }
}