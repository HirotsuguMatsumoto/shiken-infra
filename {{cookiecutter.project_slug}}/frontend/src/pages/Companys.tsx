import {
    Create,
    Datagrid,
    Edit,
    EditButton,
    List,
    SimpleForm,
    TextField,
    TextInput,
} from "react-admin";

export const CompanyList = (props: any) => (
    <List {...props} filters={[]}>
        <Datagrid>
            <TextField source="value" />
            <TextField source="id" />
            <EditButton />
        </Datagrid>
    </List>
);

export const CompanyEdit = (props: any) => (
    <Edit {...props}>
        <SimpleForm>
            <TextInput source="value" />
        </SimpleForm>
    </Edit>
);

export const CompanyCreate = (props: any) => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="value" />
        </SimpleForm>
    </Create>
);
