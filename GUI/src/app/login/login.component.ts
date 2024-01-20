import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';
import { LoginService } from '../login.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  username: string='';
  password: string='';
  errorType: string='';
  unvalidusername:boolean = false;
  unvalidpassword:boolean = false;
  loginUser: string='';

  constructor(private router: Router, private dataService: DataService, private loginService: LoginService) {}

  // Funktion überprüft, ob das Einloggen des Nutzer passt (nutzt den data.service.ts)
  login() {
    this.dataService.checkCredentials(this.username, this.password).subscribe((result) => {
      if (result == 'valid') {
        this.loginService.setloginValue(true);
        this.unvalidusername = false;
        this.unvalidpassword = false;
        const routerLink = [''];
        this.router.navigate(routerLink);
        console.log('Login of username ' + this.username + ' successful!');
      } else {
        this.dataService.getUsers().subscribe((users) => {
          const userExists = users.some((u) => u.username === this.username);

          if (userExists) {
            this.loginService.setloginValue(false);
            this.errorType = 'invalidPassword';
            this.unvalidusername = false;
            this.unvalidpassword = true;
            console.log('Login of username ' + this.username + ' not successful, because false password!');
          } else {
            this.loginService.setloginValue(false);
            this.errorType = 'invalidUsername';
            this.unvalidusername = true;
            this.unvalidpassword = true;
            console.log('Login of username ' + this.username + ' not successful, because no authorizised user!');
          }
        });
      }
    });
  }

  
}