import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

// Klasse ermöglicht einen boolean Wert zwischen Componenten auszutauschen (Login)
export class LoginService {
  private isLoggedIn: boolean = false;
  private userLoggedIn: string = '';

  getloginValue(): boolean {
    return this.isLoggedIn;
  }

  setloginValue(value: boolean): void {
    this.isLoggedIn = value;
  }

  getloginUser(): string{
    return this.userLoggedIn;
  }

  setloginUser(value: string): void {
    this.userLoggedIn = value;
  }
}