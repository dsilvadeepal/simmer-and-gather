import {useState} from 'react';
import {render,screen,fireEvent} from '@testing-library/react';
import {test,expect} from 'vitest';
import {AllergyChoices} from './AllergyChoices';
function Harness(){const [v,set]=useState<string[]|null>(null);return <><AllergyChoices value={v} onChange={set}/><output>{JSON.stringify(v)}</output></>;}
test('untouched is unknown; none is explicit and exclusive with restrictions',()=>{
 render(<Harness/>);
 expect(screen.getByRole('status')).toHaveTextContent('null');
 fireEvent.click(screen.getByLabelText('No known allergies'));
 expect(screen.getByRole('status')).toHaveTextContent('[]');
 fireEvent.click(screen.getByLabelText('Avoid nuts'));
 expect(screen.getByLabelText('No known allergies')).not.toBeChecked();
 fireEvent.click(screen.getByLabelText('Avoid gluten'));
 expect(screen.getByRole('status')).toHaveTextContent('["nuts","gluten"]');
 fireEvent.click(screen.getByLabelText('No known allergies'));
 expect(screen.getByLabelText('Avoid nuts')).not.toBeChecked();
});
