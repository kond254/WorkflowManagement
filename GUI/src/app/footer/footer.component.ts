import { Component } from '@angular/core';
import { DataRoleService } from '../dataRole.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {

  constructor(private dataroleservice: DataRoleService) {
  }

  // Function returns the boolean values of dataRole.service to enable/disable the rights for the user in UI
  get showRoleHome(): boolean {
    return this.dataroleservice.showRoleHome;
  }
  get showRoleHrdepartment(): boolean {
    return this.dataroleservice.showRoleHrdepartment;
  }
  get showRoleHrmanagement(): boolean {
    return this.dataroleservice.showRoleHrmanagement;
  }
  get showRoleAccouting(): boolean {
    return this.dataroleservice.showRoleAccouting;
  }
}
