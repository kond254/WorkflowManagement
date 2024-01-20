import { Component, inject, Input } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { LoginService } from '../login.service';
import { SnackbarService } from '../snackbar.service';
import { RoleService } from '../role.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})

export class NavbarComponent {

  constructor(public loginService: LoginService, private snackbarService: SnackbarService, private roleService: RoleService) {}

  private breakpointObserver = inject(BreakpointObserver);

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );
   
    // Funktion wird ausgeführt, wenn logout Button gedrückt wird und setzt dropdown Seiten auf standard false
    logout(){
      this.loginService.setloginValue(false);
      this.snackbarService.showSuccess('Logout erfolgreich!');
      console.log('Logout username!');

      const showRoleHome = false;
      const showRoleHrdepartment = false;
      const showRoleHrmanagement = false;
      const showRoleAccouting = false;

      this.roleService.updateRechte(showRoleHome, showRoleHrdepartment, showRoleHrmanagement, showRoleAccouting);
    }

    // Funktion ruft die boolean Werte von role.service auf
    get showRoleHome(): boolean {
      return this.roleService.showRoleHome;
    }
    get showRoleHrdepartment(): boolean {
      return this.roleService.showRoleHrdepartment;
    }
    get showRoleHrmanagement(): boolean {
      return this.roleService.showRoleHrmanagement;
    }
    get showRoleAccouting(): boolean {
      return this.roleService.showRoleAccouting;
    }
}
