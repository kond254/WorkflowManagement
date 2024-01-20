import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  username: string="";
  password: string="";
  errorType: string="";
  unvalidusername:boolean = false;
  unvalidpassword:boolean = false;

  constructor(private router: Router, private dataService: DataService) {}

  logInEmployee() {
    this.dataService.checkCredentials(this.username, this.password).subscribe((result) => {
      if (result === 'valid') {
        console.log('Login of username ' + this.username + ' successful!');
        this.unvalidusername = false;
        this.unvalidpassword = false;
        const routerLink = [''];
        this.router.navigate(routerLink);
      } else {
        this.dataService.getUsers().subscribe((users) => {
          const userExists = users.some((u) => u.username === this.username);

          if (userExists) {
            this.errorType = 'invalidPassword';
            console.log('Login of username ' + this.username + ' not successful, because false password!');
            this.unvalidusername = false;
            this.unvalidpassword = true;
          } else {
            this.errorType = 'invalidUsername';
            console.log('Login of username ' + this.username + ' not successful, because no authorizised user!');
            this.unvalidusername = true;
            this.unvalidpassword = true;
          }
        });
      }
    });
  }
}