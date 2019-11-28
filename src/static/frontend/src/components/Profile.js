import React, { Component } from "react";
import PlagiarismResultItem from './PlagiarismResultItem';
import Textarea from 'react-textarea-autosize';
import Loader from './Loader';
import OptionalAlert from './OptionalErrorAlert';

const DEFAULT_TITLE = 'мистецтво бароко';
const DEFAULT_TEXT =
`В епоху бароко живопис став більш аристократичним, барвистим і динамічним з незвичайними сюжетами. Бароко підняло мистецтво минулих епох на нову ступінь. Порівняно зі спокійною та врівноваженою епохою Відродження, бароко проникало в душу глядача і вражала її. Перший великий італійська живописець епохи бароко, Караваджо був запальною людиною, що відображалося в його творах, вони були наповнені драматизмом і експресією. Порівняно з сучасниками, які звикли до використання попередніх начерків, малював прямо з натури. Створена Караваджо система одержала широке поширення ще при житті художника. Багато художників епохи бароко наслідували стилю Караваджо.
Людина бароко, на відміну від цільних натур літератури ренесансу, є роздвоєною. Людина бароко — це, за образом англійського поета Дж. Донна, черв, який плазує у бруді та крові. І разом зі скороминучим життям приреченої людини мають загинути всі явища природи, взагалі все, що живе. Так, ліричний герой А. Ґріфіуса із захопленням дивиться на чудову троянду, але думає не про її красу, а про те, що незабаром вона зів'яне.`;

class Profile extends Component {
    constructor(...args) {
        super(...args);
        this.state = {
            title: DEFAULT_TITLE,
            text: DEFAULT_TEXT,
            output: [],
            isLoading: false
        }
    }

    onChange(e) {
        const { target } = e;
        this.setState({ [target.name]: target.value })
    }

    async onSubmit() {
        const { title, text } = this.state;
        this.setState({
            isLoading: true
        });
        let error = '';
        try {
            const result = await this.props.checkForPlagiarism({ title, text });
            this.setState({
                output: result,
                isLoading: false
            });
        } catch (e) {
            error = e.message;
            this.setState({
                isLoading: false,
                error
            })
        }
    }

    render() {
        const { output, isLoading, error } = this.state;
        return (
            <div>
                Головна сторінка <br/>
                <OptionalAlert msg={error}/>
                <input
                    type="text"
                    className="form-control"
                    name="title"
                    value={this.state.title} onChange={this.onChange.bind(this)}
                /><br/>
                <div className="input-group">
                    <Textarea
                        className="form-control"
                        aria-label="With textarea"
                        name="text"
                        onChange={this.onChange.bind(this)}
                    >{this.state.text}</Textarea>
                </div>
                <button
                    className="btn btn-primary"
                    onClick={this.onSubmit.bind(this)}
                >Підтвердити</button>
                <br/>
                {
                    isLoading
                        ? <Loader />
                        : <div>{output.map((e, i) =>
                            <PlagiarismResultItem
                                key={i}
                                number={i}
                                link={e}
                            ></PlagiarismResultItem>)}
                          </div>
                }
            </div>
        );
    }
}

export default Profile;
