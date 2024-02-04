import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

// This class allows to store the rights of the users and other components can retrieve the rights
export class RoleService {
    variable: string='';

  //Function that other components call to get the user role rights as a string
  getRoleVariable(): string {
    return this.variable;
  }

  //Function that other components call to set the user role rights as a string
  setRoleVariable(value: string): void {
    this.variable = value;
  }
}