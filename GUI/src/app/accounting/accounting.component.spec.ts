import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AccountingComponent } from './accounting.component';

describe('AccountingComponent', () => {
  let component: AccountingComponent;
  let fixture: ComponentFixture<AccountingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AccountingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should change order of invoices', () => {
    const initialOrder = [...component.invoices];

    component.changeOrder();

    expect(component.invoices).toEqual(initialOrder.reverse());
  });

  // Hier kannst du weitere Tests für die anderen Funktionen schreiben

});
