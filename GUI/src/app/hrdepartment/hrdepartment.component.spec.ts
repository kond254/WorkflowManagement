import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrdepartmentComponent } from './hrdepartment.component';

describe('HrdepartmentComponent', () => {
  let component: HrdepartmentComponent;
  let fixture: ComponentFixture<HrdepartmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrdepartmentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrdepartmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
